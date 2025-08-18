pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'backend-analysis'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = credentials('sonar-token')

        DOCKER_REGISTRY = "docker.io"
        DOCKER_IMAGE = "aptusdatalabstech/backend-service"
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
                        def projectKey = ""
                    if (env.BRANCH_NAME == "dev") {
                        projectKey = "myapp-develop"
                    } else if (env.BRANCH_NAME == "staging") {
                        projectKey = "myapp-staging"
                    } else if (env.BRANCH_NAME == "main") {
                        projectKey = "myapp"
                    } else {
                        projectKey = "myapp-feature-${env.BRANCH_NAME.replaceAll('/', '-')}"
                        
                    }
                        try {
                            sh """
                                echo "Using sonar-scanner from: ${scannerHome}"
                                ${scannerHome}/bin/sonar-scanner -X \
                                -Dsonar.projectKey=${projectKey} \
                                    -Dsonar.sources=. 
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
        stage('Unit Tests') {
    steps {
        sh """
            pip install -r requirements.txt
            pytest --maxfail=1 --disable-warnings -q
        """
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
                        $DOCKER_CREDS
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
                sshagent(['deploy-ssh']) {
                    sh """
                        chmod +x ./scripts/deploy_compose.sh
                        ./scripts/deploy_compose.sh \
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
