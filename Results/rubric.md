# Evaluation Rubric and Results Analysis

## 1. Scoring Rubric

Each generated test suite will receive a score out of 100 points.

| Category | Points | Evaluation Criteria |
|---|---:|---|
| Basic Unit Tests | 20 | Tests normal inputs and expected program behavior. |
| Edge-Case Coverage | 35 | Tests boundary conditions, unusual inputs, and predefined edge cases. |
| Error Detection | 35 | Detects known bugs that violate the intended behavior. |
| Test Execution and Correctness | 10 | Test code runs correctly and uses valid assertions and expected results. |
| **Total** | **100** | |

### Basic Unit Tests (20 points)

- **18–20:** Thoroughly tests the program's main functionality.
- **14–17:** Covers most expected behavior, with minor omissions.
- **8–13:** Covers some functionality but misses important cases.
- **1–7:** Includes very few meaningful tests.
- **0:** Includes no valid basic tests.

### Edge-Case Coverage (35 points)

Before evaluating the generated tests, create a checklist of expected edge cases for each program. Use the same checklist for every model and prompt condition.

**Formula:**

Edge-Case Score = 35 × (Number of Valid Scenarios Covered ÷ Total Number of Scenarios)

A scenario counts as covered only if a test actually exercises it and makes a meaningful assertion. Comments and duplicate tests do not count as additional coverage.

### Error Detection Using Reference Solutions (35 points)

The sample solution for each program will serve as the reference implementation for evaluating AI-generated tests. Each test suite will first be checked against the reference solution to determine whether its assertions match the intended behavior.

To evaluate bug-detection ability, deliberately introduce selected bugs into copies of the reference programs. Run each generated test suite against these buggy versions and record which bugs are detected.

A bug is considered detected when a test passes against the correct reference implementation but fails against a buggy version because the bug changes the program's behavior.

**Formula:**

Error Detection Score = 35 × (Number of Bugs Detected ÷ Total Number of Bugs Evaluated)

Only count bugs that can be meaningfully evaluated by the test suite. Tests that fail against the reference solution because of incorrect assertions should be reviewed before their bug-detection results are counted.

The same predefined buggy versions will be used for every AI model and prompt condition for a given program.

### Test Execution and Correctness (10 points)

- **9–10:** Tests execute successfully, and assertions and expected results are valid.
- **7–8:** Tests mostly work, with minor issues.
- **4–6:** Some tests execute, but notable errors or incorrect assertions exist.
- **1–3:** Major issues prevent meaningful evaluation.
- **0:** The test suite cannot be meaningfully evaluated because it is not executable.

Record execution status separately as **Pass**, **Fail**, or **Partially Runs**. Preserve the original generated code and its initial score. Any fixes made for further investigation should be recorded separately.

---

## 2. Results Recording

Create one record for each generated test suite.

| Field | Result |
|---|---|
| Run ID | |
| Program | |
| AI Model and Version | |
| Date | |
| Prompt Condition (Code-Only / Detailed / Minimal) | |
| Repetition (1 / 2 / 3) | |
| Execution Status | |
| Execution Errors | |
| Basic Unit Tests (/20) | |
| Edge-Case Coverage (/35) | |
| Error Detection (/35) | |
| Test Execution and Correctness (/10) | |
| **Total Score (/100)** | |
| Edge Cases Covered | |
| Bugs Detected | |
| Notes | |

Suggested Run ID format: `P1-ChatGPT-Detailed-R1`.

---

## 3. Results Analysis

### Average Scores by Model and Prompt Condition

Calculate the average score across the three repetitions for each model, prompt condition, and program. Review the results for each program before calculating an overall average.

| Model | Code-Only Average | Detailed-Description Average | Minimal-Description Average |
|---|---:|---:|---:|
| ChatGPT | | | |
| Claude | | | |
| Gemini | | | |

### Comparison of Individual Outcomes

Compare the average scores for each of the following:

- **Edge-Case Coverage:** Which model and prompt condition covered the most predefined edge cases?
- **Error Detection:** Which model and prompt condition detected the most predefined bugs?
- **Basic Unit Tests:** Which models consistently tested normal program behavior?
- **Test Execution and Correctness:** Which models generated test suites that executed correctly and used valid assertions?
- **Consistency:** How much did scores vary across the three repetitions?

### Research Questions

1. Did detailed requirements improve results compared with a minimal description?
2. How did the code-only prompt compare with prompts that described the program's expected behavior?
3. Did one model perform better overall, or did performance vary by program and prompt condition?
4. Were the results consistent across the three repetitions?
5. Which edge cases or bugs were most frequently missed?

### Interpreting the Results

- Apply the same scoring criteria and predefined scenarios to every model.
- Report averages alongside individual repetition scores to show variation.
- Compare each program separately before combining results, since program characteristics may affect performance.
- Interpret conclusions within the limits of the experiment. Three programs and three repetitions per condition provide a limited sample and cannot establish that one model will always perform better in other situations.