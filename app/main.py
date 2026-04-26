import os
import json
import shutil
from app.config import sourceDirectory, reportDirectory, promptDirectory, cacheDirectory
from app.llm_handler import load_instruction, generate_prompt, query_llm
from app.report_generator import generate_all_reports, print_terminal_report, save_yaml_report

def findCppFiles(sourcePath):
    cppFileList = []
    for rootDir, subdirs, fileNames in os.walk(sourcePath):
        if 'third_party' in rootDir:
            continue

        for fileName in fileNames:
            if fileName.endswith(('.cpp', '.h', '.cc')):
                fullFilePath = os.path.join(rootDir, fileName)
                cppFileList.append(fullFilePath)

    return cppFileList

def main():
    os.makedirs(reportDirectory, exist_ok=True)
    os.makedirs(cacheDirectory, exist_ok=True)

    print("C++ Test Coverage Report Generator")
    print("\nFinding C++ source files...")

    discoveredFiles = findCppFiles(sourceDirectory)
    if not discoveredFiles:
        print(f"No C++ files found in {sourceDirectory}. Exiting.")
        return

    print(f"  - Found {len(discoveredFiles)} files to analyze.")

    print("\nAnalyzing files one by one with the LLM...")

    analysisInstruction = load_instruction(os.path.join(promptDirectory, 'generate_report.yaml'))
    aggregatedAnalyses = []

    for currentFilePath in discoveredFiles:
        currentFileName = os.path.basename(currentFilePath)
        cachedResultPath = os.path.join(cacheDirectory, f"{currentFileName}.log")

        print(f"-> Analyzing '{currentFileName}'...")

        llmOutput = None

        if os.path.exists(cachedResultPath):
            with open(cachedResultPath, 'r', encoding='utf-8') as cacheFile:
                llmOutput = cacheFile.read()
            print("  [pass] - Analysis loaded from cache.")
        else:
            try:
                with open(currentFilePath, 'r', encoding='utf-8') as sourceFile:
                    sourceCodeContent = sourceFile.read()
            except Exception as readError:
                print(f"  [fail] - Error reading file: {readError}")
                continue

            analysisPrompt = generate_prompt(analysisInstruction, sourceCodeContent, currentFileName)
            llmOutput = query_llm(analysisPrompt)

            if llmOutput:
                # Validate JSON before caching to avoid storing malformed responses
                try:
                    jsonStart = llmOutput.find('{')
                    jsonEnd = llmOutput.rfind('}') + 1
                    json.loads(llmOutput[jsonStart:jsonEnd])
                    with open(cachedResultPath, 'w', encoding='utf-8') as cacheFile:
                        cacheFile.write(llmOutput)
                    print("  [pass] - Analysis successful (and saved to cache).")
                except json.JSONDecodeError:
                    print("  [warn] - LLM returned invalid JSON; response NOT cached. Will retry next run.")
                    continue
            else:
                print(f"  [fail] - Failed to get analysis for this file.\n")
                continue

        try:
            jsonStartIndex = llmOutput.find('{')
            jsonEndIndex = llmOutput.rfind('}') + 1
            cleanedJsonString = llmOutput[jsonStartIndex:jsonEndIndex]

            parsedAnalysis = json.loads(cleanedJsonString)
            aggregatedAnalyses.append(parsedAnalysis)
        except json.JSONDecodeError:
            print(f"  [fail] - Cached response for '{currentFileName}' is invalid JSON. Deleting cache entry for re-analysis.")
            if os.path.exists(cachedResultPath):
                os.remove(cachedResultPath)

    print("\nGenerating final reports...")
    if not aggregatedAnalyses:
        print("No successful analyses were completed. Cannot generate a final report.")
        return

    finalReportData = generate_all_reports(aggregatedAnalyses)
    print("  - Detailed Markdown reports have been saved in the 'reports' directory.")

    yamlReportPath = save_yaml_report(finalReportData)
    print(f"  - Final structured report saved to: {yamlReportPath}")

    print("\n")
    print_terminal_report(finalReportData)

    print("\nAll reports generated successfully!")

if __name__ == "__main__":
    main()
