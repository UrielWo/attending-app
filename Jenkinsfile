pipeline {
    agent any
    stages {
        stage('builds') {
            steps {
              sh '''
                echo 'build started'
                docker build .
                docker images
                docker system prune -a --volumes -f
              '''
            }
        }
      stage('test') {
            steps {
                sh 'deploy.sh test'
            }
        }
      stage('deploy') {
            steps {
                sh 'deploy.sh prod'
            }
        }
    }
    post {
        always {
            echo 'The pipeline completed'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}
