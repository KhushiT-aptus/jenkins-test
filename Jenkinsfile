pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'backend-analysis'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = credentials('sonar-token')

        DOCKER_REGISTRY = "info@aptusdatalabs.com.com"
        DOCKER_IMAGE = "pie/backend-service"
        DOCKER_CREDS = credentials('docker-creds')
        DEPLOY_SERVER = "aptus@192.168.1.235"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}",
                    url: 'https://github.com/KhushiT-aptus/jenkins-test.git',
                    credentialsId: 'git-cred'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarServer') {
                    script {
                        def scannerHome = tool 'sonar-scanner'
                        try {
                            sh """
                                echo "Using sonar-scanner from: ${scannerHome}"
                                ${scannerHome}/bin/sonar-scanner -X -Dsonar.projectKey=backend-analysis -Dsonar.sources=.
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

        stage('Docker Build & Push') {
            steps {
                echo "Building the project using Docker ...."
                sh """
                    chmod +x scripts/build_and_push.sh
                    ./scripts/build_and_push.sh \
                        $DOCKER_REGISTRY/$DOCKER_IMAGE:${BUILD_NUMBER} \
                        $DOCKER_REGISTRY \
                        $DOCKER_CREDS_PSW \
                        $DOCKER_CREDS_USR
                """
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
                sshagent(['deploy-ssh']){
                   sh """
                       chmod +x ./scripts/deploy_compose.sh \
                            $DEPLOY_SERVER \
                            $DOCKER_REGISTRY \
                            $DOCKER_IMAGE \
                            ${BUILD_NUMBER} \
                            $DOCKER_CREDS_USR \
                            $DOCKER_CREDS_PSW
                    """
                }
            }
        }
    }
}
