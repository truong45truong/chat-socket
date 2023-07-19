import type { AxiosProgressEvent, AxiosResponse, GenericAbortSignal } from 'axios'
import request from './axios'
import { useAuthStore } from '@/store'

export interface HttpOption {
  url: string
  data?: any
  method?: string
  headers?: any
  onDownloadProgress?: (progressEvent: AxiosProgressEvent) => void
  signal?: GenericAbortSignal
  beforeRequest?: () => void
  afterRequest?: () => void
}

export interface Response<T = any> {
	response: any
  data: T
  message: string | null
  status: string
}

function http<T = any>(
  { url, data, method, headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
) {
  const successHandler = (res: AxiosResponse<Response<T>>) => {

		if (res.status === 200 || res.status === 201 || res.status === 204 || typeof res.data === 'string') {
			return res.data
		}


    return Promise.reject(res)
  }

  const failHandler = (error: Response<Error>) => {
		const authStore = useAuthStore()

		afterRequest?.()
    
		if (error?.response?.status === 401) {
			authStore.removeAuth()
		}

		throw new Error(error?.response?.data?.detail || error?.message || 'Error', {cause: error?.response?.status})
  }

  beforeRequest?.()

  method = method || 'GET'

  const params = Object.assign(typeof data === 'function' ? data() : data ?? {}, {})

	if (method === 'GET') {
		return request.get(url, { params, signal, onDownloadProgress }).then(successHandler, failHandler)
	} else if (method === 'POST') {
		return request.post(url, params, { headers, signal, onDownloadProgress }).then(successHandler, failHandler)
	} else if (method === 'PUT') {
		return request.put(url, params, { headers, signal, onDownloadProgress }).then(successHandler, failHandler)
	} else {
		return request.delete(url, params).then(successHandler, failHandler)
	}

}

export function get<T = any>(
  { url, data, method = 'GET', onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}

export function post<T = any>(
  { url, data, method = 'POST', headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    headers,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}

export function put<T = any>(
  { url, data, method = 'PUT', headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    headers,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}

export function destroy<T = any>(
  { url, data, method = 'DELETE', headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    headers,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}


export default post