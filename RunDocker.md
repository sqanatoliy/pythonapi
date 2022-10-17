"""
- Перевірити встановлений Docker > docker --version
- Встановити образ Python > docker pull python
- Створити Dockerfile в корені проекту для створення образу для запуску тестів
- для створення образу тестів виконати > docker build -t pytest_runner .
- Запустити контейнер > docker run -rm --mount type=bind,src=C:\projects\pythonapi,target=/tests_project/ pytest_runner
- де src - місце з якого копіюються тести, target - куди копіюються тести.
- створити docker-compose.yml
- запускати командою > docker-compose up --build
- 
"""