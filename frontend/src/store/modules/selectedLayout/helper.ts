
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
  view_reponsice : {
    isSelectLayouMenu : boolean
  }
  view_show_menu_reponsive : {
    isShowMenu : boolean
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
    },
    view_reponsice : {
      isSelectLayouMenu : false
    },
    view_show_menu_reponsive : {
      isShowMenu : false
    }
  }
}


