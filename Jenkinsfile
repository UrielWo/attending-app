pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
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
}
