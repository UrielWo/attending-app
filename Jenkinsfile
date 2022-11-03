pipeline {
    agent any
    stages {
        stage('builds') {
            steps {
              sh '''
                echo 'build started'
                docker build --tag urielwo/final_project .
                docker images
              '''
              //docker system prune -a --volumes -f
              // push image to docker hub before prune
            }
        }
      stage('test') {
            steps {
                sh 'bash deploy.sh test'
            }
        }
      stage('deploy') {
            steps {
                sh 'bash deploy.sh prod'
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
