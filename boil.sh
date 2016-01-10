function boil ()
{
  REPO=$1
  tmp="tmpzip"
  tmpzip="tmp.zip"

  echo "Repo: $REPO"
  #if [[ $REPO =~ .*\/.* ]] && echo "match" || echo "bad"a

  # download the repo master as zip file
  zipurl="https://github.com/$REPO/archive/master.zip"
  curl $zipurl -L0ko $tmpzip

  # unzip folder to tmp
  unzip $tmpzip -d ./$tmp

  # get name of the internal folder
  folder=$(ls $tmp)

  for obj in $( ls "$tmp/$folder" ); do
    #kjecho $obj
    cp -R "$tmp/$folder/$obj" .
  done

  rm -rf tmpzip
}
