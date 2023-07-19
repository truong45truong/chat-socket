export interface SettingState {
  isShow: boolean | undefined ,
  lang : string ,
}

export function getSettingState() : SettingState {
  return {
    isShow : false ,
    lang : 'VN',
  }
}


