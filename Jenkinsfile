pipeline {
    agent any

    environment {
        PATH = "/usr/bin:/usr/local/bin:${env.PATH}"
        KUBECONFIG = "${env.HOME}/.jenkins/kubeconfig"
        STAGING_URL = 'http://8.217.228.180:30080'
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
                        export PATH="/usr/bin:/usr/local/bin:/snap/bin:\$PATH"
                        KUBECTL=\$(command -v kubectl 2>/dev/null)
                        [ -z "\$KUBECTL" ] && KUBECTL="/usr/bin/kubectl"
                        [ ! -x "\$KUBECTL" ] && echo "kubectl not found. Install: sudo apt install -y kubectl" && exit 1
                        echo "Using kubectl: \$KUBECTL"
                        \$KUBECTL apply -f k8s/namespace.yaml
                        sed -e 's|PLACEHOLDER_IMAGE|${image}|' k8s/demo-server-deployment.yaml | \$KUBECTL apply -f -
                        \$KUBECTL apply -f k8s/demo-server-service.yaml
                        \$KUBECTL rollout status deployment/demo-server -n staging --timeout=120s
                    """
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh """
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -q -r api_auto/requirements.txt
                    cd api_auto && BASE_URL=${env.STAGING_URL} pytest -m smoke -v --tb=short
                """
            }
        }
    }
}
