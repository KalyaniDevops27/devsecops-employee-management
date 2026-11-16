# GitHub Actions CI Failure – Troubleshooting Report

## 1. Overview

As part of the DevSecOps Employee Management project, I performed a controlled CI troubleshooting exercise to understand how GitHub Actions detects test failures and how to investigate them.

**Project:** DevSecOps Employee Management API  
**CI Tool:** GitHub Actions  
**Testing Framework:** Pytest  
**Branch:** `feature/ci-practice`  
**Pull Request:** [PR #1](https://github.com/KalyaniDevops27/devsecops-employee-management/pull/1)

This was a deliberately introduced test failure for learning and troubleshooting purposes, not a production incident.

## 2. Initial Problem

I introduced an intentional assertion failure in a temporary test case.

The test expected:

```python
expected_status = "healthy"
```

But the actual value was:

```python
actual_status = "unhealthy"
```

The assertion failed because the expected and actual values did not match.

## 3. Symptoms Observed

The local test execution reported:

AssertionError: assert 'unhealthy' == 'healthy'

- 14 tests passed.
- 1 test failed.
- Pytest returned exit code 1.

GitHub Actions reported the same test failure on its hosted runner.

## 4. Investigation

I followed a step-by-step troubleshooting approach.

1. Executed the test locally using `pytest -v`.
2. Identified the failing test from the pytest output.
3. Examined the assertion error.
4. Checked the GitHub Actions execution logs.
5. Compared local execution with the GitHub-hosted runner.
6. Confirmed that the failure was caused by the deliberately incorrect test assertion.

### Important observation

The Starlette/httpx deprecation warning was also visible in the test output, but it was not responsible for the CI failure.

## 5. Root Cause

The root cause was an incorrect expected value in the temporary test case.

It was not caused by:

- Application code.
- GitHub Actions configuration.
- Python installation.
- GitHub-hosted runner availability.

## 6. Resolution

I corrected the assertion and verified that the test passed.

The subsequent test execution passed all 15 tests, including the temporary troubleshooting test.

After completing the exercise, I removed the temporary failure test to keep the application's permanent test suite clean.

The final test suite returned to its original 14 tests.

## 7. Final Verification

The final GitHub Actions execution completed successfully:

- 14 tests passed.
- 0 tests failed.
- CI workflow successful.
- Pull Request checks passed.
- Changes merged into the `main` branch.

## 8. Technical Learnings

Through this exercise, I strengthened my understanding of:

- GitHub Actions workflow execution.
- Pytest failure analysis.
- Reading and interpreting CI logs.
- Process exit codes and CI job status.
- Local versus hosted runner behaviour.
- Feature branches and Pull Request workflows.
- Distinguishing actual failures from non-blocking warnings.

## 9. Preventive Practices

- Execute automated tests locally before pushing changes.
- Review CI logs instead of assuming every failure is an application issue.
- Keep temporary troubleshooting tests separate from permanent application tests.
- Use Pull Requests and automated checks before merging into the main branch.
- Investigate warnings separately from test failures.

## 10. Conclusion

This exercise helped me understand that troubleshooting a CI pipeline requires more than identifying an error message.

A systematic approach involves observing the failure, analysing logs, isolating the problem, identifying the root cause, validating the correction, and preventing similar issues in future executions.
