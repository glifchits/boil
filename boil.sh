function boil ()
{
  REPO=$1
  tmp="tmpzip"
  tmpzip="tmp.zip"

  if [[ $REPO =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$ ]]; then
  else
    echo "Usage: $0 [github repo]"
    echo "  [github repo] is of the format {username}/{repository}"
    return
  fi

  # download the repo master as zip file
  zipurl="https://github.com/$REPO/archive/master.zip"
  echo "Downloading $REPO:master"
  curl $zipurl -L0ko $tmpzip &> /dev/null

  # unzip folder to tmp
  echo "Unzipping..."
  unzip $tmpzip -d ./$tmp &> /dev/null

  # get name of the internal folder
  folder=$(ls $tmp)

  for obj in $( ls "$tmp/$folder" ); do
    cp -R "$tmp/$folder/$obj" .
  done

  echo "done. cleaning up"
  rm -rf $tmpzip $tmp
}
