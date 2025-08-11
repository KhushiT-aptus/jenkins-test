pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'backend-analysis'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}",
                    url: 'https://github.com/KhushiT-aptus/jenkins-test.git',
                    credentialsId: 'git-cred'
            }
        }

        stage('Build') {
            steps {
                echo 'Building project...'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarServer') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'dev'
                    branch 'pre-prod'
                    branch 'main'
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        echo 'deploying project... to dev'
                    } else if (env.BRANCH_NAME == 'staging') {
                        echo 'Building project... to uat'
                    } else if (env.BRANCH_NAME == 'main') {
                       echo 'deploying to main'
                    }
                }
            }
        }
    }
}
