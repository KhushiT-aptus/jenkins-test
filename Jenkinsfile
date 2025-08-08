pipeline {
    agent any

    tools {
        git 'Default'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/KhushiT-aptus/jenkins-test.git', 
                    credentialsId: 'git-cred'
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
