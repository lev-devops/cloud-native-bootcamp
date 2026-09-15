pipeline {
  agent any
  stages {
    stage('Test') { steps { sh 'cd app && npm test' } }
    stage('Build') { steps { sh 'docker build -f docker/Dockerfile -t "$IMAGE_REPOSITORY:${BUILD_NUMBER}" .' } }
  }
}
