# Log Analyzer

A simple Python CLI tool that analyzes log files, supports filtering, and generates summary reports.


## How to Run

###### 1. Clone the repository
```bash
git clone https://github.com/Alicade123/log-analyzer.git
cd log-analyzer
```
###### 2. Analyze entire log file
```bash
python log_analyzer.py -file app.log
```
###### 4. Show only errors
```bash
python log_analyzer.py -file app.log --level ERROR
```
###### 6. Filter by time range
```bash
python log_analyzer.py -file app.log --from_time "2024-01-15 10:00" --to_time "2024-01-15 11:00"
```
###### 8. Export summary
```bash
python log_analyzer.py -file app.log -export summary.csv
```
