pipeline {
    agent any

    tools {
        git 'Default'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/your-username/your-repo.git', 
                    credentialsId: 'github-credentials'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
                sh 'ls -la'
            }
        }
    }
}
