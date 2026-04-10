import apiClient from "@/utils/apiClient"

export default {
  uploadImage(file) {
    const formData = new FormData()
    formData.append("file", file)
    return apiClient.post("/media/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
}
