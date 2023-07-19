import { ss } from '@/utils/storage'

const LOCAL_NAME = 'BG-CHAT'

export interface BgState {
  image: any | undefined ,
  isSelect : string | undefined
}
export function setBG(url : string) {
  return ss.set(LOCAL_NAME, url) 
}

export function removeBG() {
  return ss.remove(LOCAL_NAME)
}
export function getBG() : BgState {
  return {
    image : [
      {
        url : './../../../src/assets/images/display/bg-1.jpg'
      },
      {
        url : './../../../src/assets/images/display/bg-2.jpg'
      },
      {
        url : './../../../src/assets/images/display/bg-3.jpg'
      },
      {
        url : './../../../src/assets/images/display/bg-4.jpg'
      },
    ],
    isSelect : ss.get(LOCAL_NAME) ||  './../../../src/assets/images/display/bg-4.jpg'
  }
}


