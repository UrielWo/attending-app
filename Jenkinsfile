pipeline {
    agent any
    /*environment {
        RVM_USER = credentials('RVM_USER')
        RVM_PASSWORD = credentials('RVM_PASSWORD')
        RVM_IP = credentials('RVM_PASSWORD')
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
        MYSQL_HOST = credentials('MYSQL_HOST')
        MYSQL_DB = credentials('MYSQL_DB')
        MYSQL_USER = credentials('MYSQL_USER')
        MYSQL_PASSWORD = credentials('MYSQL_PASSWORD')
    }*/
    stages {
        stage('builds') {
            steps {
              sh '''
                echo 'build started'
                docker build .
                docker images
                git add .
                git commit -m "1"
                git push 
                docker system prune -a --volumes -f
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
