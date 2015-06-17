ProtoGenDir=gen/protobuf
ProtoDir=proto

[ -d $ProtoGenDir ]; rm -rf $ProtoGenDir && mkdir -p $ProtoGenDir

for file in $(find $ProtoDir/ -name '*.proto')
do
    protoc --proto_path=$ProtoDir --python_out=$ProtoGenDir $file
done
