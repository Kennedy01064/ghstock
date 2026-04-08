import { ref } from "vue"
import catalogApi from "@/api/catalog.api"
import { useUiStore } from "@/stores/uiStore"
import { defaultProductUrl } from "@/utils/formatters"

/**
 * Encapsulates the web scraping logic for product discovery.
 */
export function useProductScraper() {
  const uiStore = useUiStore()
  
  const isDynamicModalOpen = ref(false)
  const dynamicUrl = ref("")
  const dynamicPreview = ref(null)
  const isPreviewLoading = ref(false)
  const isSubmitting = ref(false)

  const openScraper = () => {
    isDynamicModalOpen.value = true
  }

  const closeScraper = () => {
    isDynamicModalOpen.value = false
    dynamicUrl.value = ""
    dynamicPreview.value = null
    isPreviewLoading.value = false
    isSubmitting.value = false
  }

  const preview = async () => {
    const url = dynamicUrl.value?.trim()
    if (!url) {
      uiStore.warning("Ingresa un enlace valido para continuar.", "Atencion corporativa")
      return
    }

    isPreviewLoading.value = true
    dynamicPreview.value = null

    try {
      const { data } = await catalogApi.preview(url)
      dynamicPreview.value = data
      return data
    } catch (error) {
      uiStore.error(error.message, "Fallo de protocolo")
    } finally {
      isPreviewLoading.value = false
    }
  }

  const saveToCatalog = async (createAction) => {
    if (!dynamicPreview.value) return
    
    isSubmitting.value = true
    try {
      await createAction({
        sku: dynamicPreview.value.sku || null,
        name: dynamicPreview.value.name || "Producto dinamico",
        description: dynamicPreview.value.description || null,
        precio: Number(dynamicPreview.value.price || 0),
        imagen_url: dynamicPreview.value.image_url || defaultProductUrl,
        source_url: dynamicUrl.value.trim(),
        is_dynamic: true,
        unit: "Unidad",
      })
      uiStore.success(`${dynamicPreview.value.name} fue vinculado al catalogo.`, "Importacion completada")
      closeScraper()
    } catch (error) {
      // Error is usually handled by useApi or the store, but we catch it here to reset isSubmitting
      console.error("[Scraper] Save failed:", error)
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    isDynamicModalOpen,
    dynamicUrl,
    dynamicPreview,
    isPreviewLoading,
    isSubmitting,
    openScraper,
    closeScraper,
    preview,
    saveToCatalog
  }
}
