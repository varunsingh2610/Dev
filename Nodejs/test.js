
const blobStorage = require('@azure/storage-blob')
const config = require('./config');


const _getBlobConfig = () => {
    const accountName = config.ACCOUNT_NAME
    const accountKey = config.ACCOUNT_KEY
    const sharedKeyCred = new blobStorage.StorageSharedKeyCredential(
      accountName,
      accountKey
    )
  
    return {
      accountName,
      accountKey,
      sharedKeyCred,
      blobServiceURL: `https://${accountName}.blob.core.windows.net`,
      containerName: config.CONTAINER_NAME
    }
  }

  const _getBlockBlobClient = (blobName) => {
    const blobConfig = _getBlobConfig()
  
    const blockBlobClient = new blobStorage.BlobServiceClient(
      blobConfig.blobServiceURL,
      blobConfig.sharedKeyCred
    )
      .getContainerClient(blobConfig.containerName)
      .getBlobClient(blobName)
      .getBlockBlobClient()
  
    return blockBlobClient
  }
  
  const azureDownload = async (blobName) => {
    try {
      const blockBlobClient = _getBlockBlobClient(blobName)
      const downloadResponse = await blockBlobClient.download(0)
      return downloadResponse
    } catch (e) {
      console.log(e)
      throw new Error('Download failed')
    }
  }

  const downloadResponse = azureDownload("Test.txt")

  console.log(downloadResponse)


//   const getBreeds = async () => {
//     try {
//         const downloadResponse = await azureDownload("Test.txt")
//         console.log(downloadResponse)
//     } catch (error) {
//       console.error(error)
//     }
//   }

//   getBreeds()