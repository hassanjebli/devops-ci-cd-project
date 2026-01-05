pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t crud-app .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm devops-app pytest'
            }
        }

        stage('Deploy Application') {
            steps {
                sh 'docker rm -f crud-app || true'
		sh 'docker run -d --name crud-app -p 5001:5000 crud-app'
            }
        }
    }
}
