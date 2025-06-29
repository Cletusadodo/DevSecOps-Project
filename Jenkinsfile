pipeline {
    agent any
    tools {
        jdk 'jdk17'
        nodejs 'node16'
    }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/Cletusadodo/DevSecOps-Project.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    $SCANNER_HOME/bin/sonar-scanner \
                    -Dsonar.projectName=Netflix \
                    -Dsonar.projectKey=Netflix
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }

        stage('OWASP FS Scan') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage('TRIVY FS Scan') {
            steps {
                sh 'trivy fs . > trivyfs.txt 2>&1'
            }
        }

        stage('Install Gitleaks & Run Secrets Scan') {
            steps {
                sh '''
                curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest \
                | grep "browser_download_url.*linux_x64.tar.gz" \
                | cut -d '"' -f 4 \
                | wget -qi -
                ls gitleaks_*_linux_x64.tar.gz | xargs tar -xvzf
                gitleaks detect --source=. --report-path=gitleaks-report.json --exit-code 0
                '''
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker', toolName: 'docker') {
                            sh """
                            docker build --build-arg TMDB_V3_API_KEY=6a5b8ed6f09a649986892715cc1b0b38 -t netflix .
                            docker tag netflix cletusadodo/netflix:latest
                            docker push cletusadodo/netflix:latest
                            """
                    }
                }
            }
        }

        stage('TRIVY Image Scan') {
            steps {
                sh 'trivy image cletusadodo/netflix:latest > trivyimage.txt 2>&1'
            }
        }

        stage('Deploy to Container') {
            steps {
                sh 'docker run -d --name netflix -p 8081:80 cletusadodo/netflix:latest'
            }
        }
    }
}
