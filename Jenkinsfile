pipeline {
    agent any

    environment {
        KUBECONFIG = "${env.HOME}/.jenkins/kubeconfig"
        STAGING_URL = 'http://47.238.30.242:30080'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                        docker build -f demo_server/Dockerfile -t $DOCKER_USERNAME/demo-server:${BUILD_NUMBER} .
                        docker push $DOCKER_USERNAME/demo-server:${BUILD_NUMBER}
                        echo "DOCKER_IMAGE=$DOCKER_USERNAME/demo-server:${BUILD_NUMBER}" > env.txt
                    '''
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                script {
                    def image = readFile('env.txt').trim().split('=')[1]
                    sh """
                        kubectl apply -f k8s/namespace.yaml
                        sed -e 's|PLACEHOLDER_IMAGE|${image}|' k8s/demo-server-deployment.yaml | kubectl apply -f -
                        kubectl apply -f k8s/demo-server-service.yaml
                        kubectl rollout status deployment/demo-server -n staging --timeout=120s
                    """
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh """
                    pip install -q -r api_auto/requirements.txt
                    cd api_auto && BASE_URL=${env.STAGING_URL} pytest -m smoke -v --tb=short
                """
            }
        }
    }
}
