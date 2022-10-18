pipeline {
    agent any
    stages {
        stage('build') {
            steps {
               sh './build_Script.sh'
            }
        }
      stage('test') {
            steps {
                echo 'some tesdting'
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
