# autonomize-qa
QA Automation Suite for Autonomize AI Agentic Platform.

## How to Run
pip install -r requirements.txt
pytest tests/ -v

## Project Structure
- tests/        — all test files
- fixtures/     — sample patient test data (JSON)
- reports/      — auto generated HTML reports
- ci/           — Azure Pipelines CI/CD config

## Running in Docker
docker build -t autonomize-qa .
docker run autonomize-qa pytest tests/ -v