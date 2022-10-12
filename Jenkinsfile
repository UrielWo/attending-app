pipeline {
    agent any
    stages {
        stage('build') {
            steps {
               sh '/home/uriel/branch/Course-Project/build_Script.sh'
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
