#!/bin/bash

PACKAGE_DIR='./dist/package'
ZIP_FILE_NAME=lmbd.zip
ZIP_FILE_DIR="./dist/lmbd_fns/$ZIP_FILE_NAME"

function clean_dist_dir() {
  if [ -d "$PACKAGE_DIR" ]
  then
    rm -rf "$PACKAGE_DIR"
  fi
  rm $ZIP_FILE_DIR
}

function start_environment() {
  source ./environ/bin/activate
}

function create_dir() {
  if [ -d "$1" ]
  then
    return
  fi
  mkdir $1
}

function create_main() {
  touch $PACKAGE_DIR'/app.py'
  echo "$1" > $PACKAGE_DIR'/app.py'
}

# @$1 - name of function on aws.
# @$2 - name of folder to store fn code locally
function deploy() {
  FN_LOCAL_STORE_DIR="./dist/lmbd_fns/$2"
  cd $PACKAGE_DIR || exit 1;
  zip -r ../lmbd_fns/$ZIP_FILE_NAME .
  cd ../..
  if [ -d "$FN_LOCAL_STORE_DIR" ]
  then
    rm -rf "$FN_LOCAL_STORE_DIR"
  fi
  mkdir "$FN_LOCAL_STORE_DIR"
  # shellcheck disable=SC2086
  cp -r "$PACKAGE_DIR"/* "$FN_LOCAL_STORE_DIR"
  aws lambda update-function-code --function-name "$1" --zip-file fileb://dist/lmbd_fns/$ZIP_FILE_NAME
  clean_dist_dir
}

function deploy_unzip_fn() {
  DTTP_DIR='./src/dttp/'
  DTTP_DEST_DIR='./dist/package/dttp/'
  # shellcheck disable=SC2206
  PACKAGE_ARRAY=('aws' 'dao' 'models' 'service' 'utils')
  start_environment
  pip install --target $PACKAGE_DIR wheel psycopg2-binary SQLAlchemy==1.3.23 boto3==1.17.12
  # shellcheck disable=SC2128
  create_dir $DTTP_DEST_DIR
  for i in "${PACKAGE_ARRAY[@]}"
  do
    create_dir $DTTP_DEST_DIR
    cp -r "$DTTP_DIR$i" "$DTTP_DEST_DIR"
  done
  cp $DTTP_DIR'dttp_bulk.py' $DTTP_DEST_DIR
  #cp $DTTP_D
  cp ./src/secret.json $PACKAGE_DIR
  create_main $'from dttp.aws.lmb_fns import dttp_unzip_fn\ndef lambda_handler(event, context):\n\tdttp_unzip_fn(event, context)'
  deploy dttp-unzip unzip_fn
  deactivate
}

function deploy_png_fn() {
  cp /etc/ImageMagick-6/policy.xml .
  cat ./png_convert_docker.txt > Dockerfile
  docker rmi png_convert_fn
  docker rmi png_convert_fn:latest 008274210142.dkr.ecr.us-east-2.amazonaws.com/png_convert_fn:latest
  docker build -t png_convert_fn .
  docker tag png_convert_fn:latest 008274210142.dkr.ecr.us-east-2.amazonaws.com/png_convert_fn:latest
  rm policy.xml
  sudo aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin 008274210142.dkr.ecr.us-east-2.amazonaws.com
  docker push 008274210142.dkr.ecr.us-east-2.amazonaws.com/png_convert_fn:latest
}



while getopts ":d:" opt; do
  case $opt in
    d)
      case $OPTARG in
        unzip)
          deploy_unzip_fn
          ;;
        png)
          deploy_png_fn
          ;;
        *)
          echo "Invalid argument: $OPTARG" >&2
          exit 1
          ;;
      esac
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires and argument" >&2
      exit 1
      ;;
  esac
done
