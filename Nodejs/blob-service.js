
const { BlobServiceClient, StorageSharedKeyCredential, generateBlobSASQueryParameters, SASProtocol, BlobSASPermissions } = require('@azure/storage-blob')

async function main () {
  console.log('Tareen Azure Blob Service Example')
  console.log('\nConnecting to Azure Blob Service...')

  // Get Azure Storage Account Name and Storage Account Key from Environment Variables
  // (set these two variables manually in your environment to run this example locally)
  //
  // These are set in Kubernetes Secret 'tareen-storage-account-secret' in 'tareen' namespace by the configure Blob Storage DevOps pipeline.
  // This secret should be added to Kubernetes Manifest of the Backend App, so that it's visible to the application as environment variables or as a volume.
  // ( https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume )
  //
  // When AD authentication is in place , we should consider changing this approach to use User Delegation SAS tokens instead, see following for more:
  // https://docs.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas
  const account = "storagebusinesstravel"
  const accountKey = "RCV4bjqaCAvUB6aL8WrdeZ7UYBSlE1E3eedrSouE2cIsOsxfRGGM1VreBpgtRDRBP+oJWp7HhHNl1w1BdNNxlA=="
  // create new shared key credential with storage account name and key
  // with this you can create and sign new SAS tokens
  const sharedKeyCredential = new StorageSharedKeyCredential(account, accountKey)

  // Create the URL to Azure Blob Service
  const blobServiceURL = `https://${account}.blob.core.windows.net`
  console.log('Blob Service URL:' + blobServiceURL)

  // Name of the Azure Storage Blob Service Container containing Tareen Attachment Blobs:
  const TAREEN_CONTAINER = 'tax-base-test'

  // Create BlobServiceClient instance using the blobServiceURL and SharedKeyCredential
  const blobServiceClient = new BlobServiceClient(
    blobServiceURL,
    sharedKeyCredential
  )

  // List all containers in the Blob Service (there should be only one, tareen-attach)
  let i = 1
  for await (const container of blobServiceClient.listContainers()) {
    console.log(`Container ${i++}: ${container.name}`)
  }
  console.log('OK - Connected to BlobService in this Storage Account: ' + blobServiceClient.accountName)

  // Get a container Client to Tareen container and list all blobs
  // This is an example how to access blob storage content from the backend with the account key
  // (THIS APPROACH SHOULD BE USED WITH EXTREME CARE ! )
  const containerClient = await blobServiceClient.getContainerClient(TAREEN_CONTAINER)
  console.log('OK - Found container: ' + containerClient.containerName)

  console.log('Listing all blobs in the container, before uploading any...')
  var blobName = ''
  // List the blob(s) in the container.
  for await (const blob of containerClient.listBlobsFlat()) {
    console.log('\t', blob.name)
    blobName = blob.name
  }

  console.log('Uploading a new test blob to container from the backend...')
  //
  // Create a test blob and upload it from the backend - see SDK documentation for more info
  //
  var myDate = new Date().getTime()
  // create some dummy content to blob :
  const content = 'This is a Tareen test document stored from Blob example code ' + myDate
  // example blob name, with 'virtual folder path' included in the blob name :
  const newBlobName = 'TareenTestClientOy/testuser/testblobcontent_' + myDate
  const blobClient = containerClient.getBlobClient(newBlobName)

  const blockBlobClient = blobClient.getBlockBlobClient()
  const uploadBlobResponse = await blockBlobClient.upload(content, content.length)

  //
  // Add some example metadata to the new blob.
  // Adding some metadata to blobs is probably a good idea for traceability etc.
  //
  const metadata = {
    tareenCustomer: 'TareenTestClientOy',
    tareenUploadClient: 'TareenBlobTestApp',
    tareenUploadedBy: 'TareenDeveloper'
  }
  await blockBlobClient.setMetadata(metadata)

  console.log(`Uploaded block blob ${newBlobName} successfully with requestId:`, uploadBlobResponse.requestId)

  console.log('Creating temporary URL with SAS token to allow downloading of the Blob for the validity period of the SAS token...')

  //
  // Create SAS token and URL to newly created blob.
  // You should also be able create a SAS token for a Blob that has not been uploaded yet with similar approach
  //
  // Prepare SAS token with start and expiration times, permissions and other restrictions
  //
  const now = new Date()
  now.setMinutes(now.getMinutes() - 5) // set SAS token validity start time 5 minutes in past, to fix any clock skew in server
  const expiry = new Date()
  expiry.setMinutes(expiry.getMinutes() + 30) // set SAS token expiry to 30 minutes from now

  // generate SAS token, for details see :  https://docs.microsoft.com/en-us/javascript/api/@azure/storage-blob/blobsassignaturevalues?view=azure-node-latest
  const blobSAS = generateBlobSASQueryParameters(
    {
      blobName: newBlobName,
      cacheControl: 'cache-control-override',
      containerName: TAREEN_CONTAINER,
      contentDisposition: 'content-disposition-override',
      contentEncoding: 'content-encoding-override',
      contentLanguage: 'content-language-override',
      contentType: 'content-type-override',
      expiresOn: expiry, // set the time when the SAS token expires
      ipRange: { start: '0.0.0.0', end: '255.255.255.255' }, // set the allowed IP address range where the Blob can be accessed
      permissions: BlobSASPermissions.parse('r').toString(), // only read permissions - see possible other values : https://docs.microsoft.com/en-us/javascript/api/@azure/storage-blob/blobsaspermissions?view=azure-node-latest
      protocol: SASProtocol.Https, // only HTTPS allowed - see : https://docs.microsoft.com/en-us/javascript/api/@azure/storage-blob/sasprotocol?view=azure-node-latest
      startsOn: now // set the time when the SAS token validity starts
    }, sharedKeyCredential
  )

  // create URL with the SAS token which can be used to access the newly created blob as long as the token is valid
  const blobTempURL = blobServiceURL + '/' + TAREEN_CONTAINER + '/' + newBlobName + '?' + blobSAS.toString()
  console.log('\n\nYou can access the newly created Blob for 30 minutes with the URL below (copy paste to your browser):')
  console.log(blobTempURL)
}

main().then(() => console.log('\nSuccessfully executed example')).catch((ex) => console.log(ex.message))
