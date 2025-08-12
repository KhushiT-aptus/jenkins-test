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
                    script {
                        def scannerHome = tool 'sonar-scanner'
                        def projectKey = ""
                    if (env.BRANCH_NAME == "dev") {
                        projectKey = "myapp-develop"
                    } else if (env.BRANCH_NAME == "staging") {
                        projectKey = "myapp-staging"
                    } else if (env.BRANCH_NAME == "main") {
                        projectKey = "myapp"
                    } else {
                        echo "Branch not mapped to Sonar project, skipping Sonar analysis."
                        return
                    }
                        try {
                            sh """
  echo "Using sonar-scanner from: ${scannerHome}"
  ${scannerHome}/bin/sonar-scanner -X \
   -Dsonar.projectKey=${projectKey} \
    -Dsonar.sources=. \
    -Dsonar.branch.name=${env.BRANCH_NAME}
"""

                        } catch (Exception e) {
                            echo "SonarQube analysis failed: ${e}"
                            throw e
                        }
                    }
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
