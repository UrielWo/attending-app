pipeline {
    agent any
    stages {
        stage('builds') {
            steps {
              sh '''
                docker-compose up
              '''
            }
        }
      stage('test') {
            steps {
                echo 'some testing'
            }
        }
      stage('deploy') {
            steps {
                echo 'deploing'
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
