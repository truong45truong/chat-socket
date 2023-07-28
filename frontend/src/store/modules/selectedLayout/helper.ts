
export interface selectLayoutState {
  show : {
    isShowChat : boolean ,
    isShowFriend : boolean ,
    isShowGroup : boolean ,
    isShowNotification : boolean
  }
  view_layout : {
    isShowCreateGroup : boolean,
    isShowConversation : boolean
  }
}

export function getSelectLayoutState() : selectLayoutState {
  return {
    show : { 
      isShowChat : true ,
      isShowFriend : false ,
      isShowGroup : false ,
      isShowNotification : false,
    },
    view_layout : {
      isShowCreateGroup : false ,
      isShowConversation : false
    }
  }
}


