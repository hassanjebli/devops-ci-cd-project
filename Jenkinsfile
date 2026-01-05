pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devops-app .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm devops-app pytest'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker run -d -p 5001:5000 devops-app || true'
            }
        }
    }
}
