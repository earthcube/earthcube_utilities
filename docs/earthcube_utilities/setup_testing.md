# testing


To create test data, we will need to setup some test datasets.

Sometime we will need to setup an s3 mock to do this.


Right now, we can rclone.
* bucket testdata is a source DO NOT RUN TESTS OVER TESTDATA
* bucker test this is the data that should be run over
Rclone only supports a one-time sync of metadata. This means that metadata will be synced from the source object to the destination object only when the source object has changed and needs to be re-uploaded. If the metadata subsequently changes on the source object without changing the object itself then it won't be synced to the destination object. This is in line with the way rclone syncs Content-Type without the --metadata flag.


Log onto geocodes-aws-dev.earthcube.org
Use rclone to 'sync'
 rclone delete awsdev:test/summoned/geocodes_demo_datasets
 rclone delete  awsdev:test/summoned/iris
 rclone delete  awsdev:test/milled/geocodes_demo_datasets
 rclone delete  awsdev:test/milled/iris

 rclone copy -M  awsdev:testdata/summoned/geocodes_demo_datasets awsdev:test/summoned/geocodes_demo_datasets
  rclone copy -M  awsdev:testdata/summoned/geocodes_demo_datasets awsdev:test/summoned/geocodes_demo_datasets_set2
 rclone copy -M  awsdev:testdata/summoned/iris awsdev:test/summoned/iris
 rclone copy -M  awsdev:testdata/milled/geocodes_demo_datasets awsdev:test/milled/geocodes_demo_datasets
 rclone copy -M  awsdev:testdata/milled/iris awsdev:test/milled/iris


big clone
 rclone copy -M  awsdev:testdata/summoned/magic awsdev:test/summoned/magic

 rclone copy -M awsdev:testdata/summoned/geocodes_demo_datasets awsdev:test/summoned/geocodes_demo_datasets
 rclone copy -M production:gleaner-wf/summoned/iris awsdev:testdata/summoned/iris    
rclone copy -M production:gleaner-wf/milled/iris awsdev:testdata/milled/iris
earthcube@ip-1
