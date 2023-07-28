export interface Notification {
    content : string ,
    email_user_chat : string ,
    is_chat : boolean ,
    type : string ,
    group_id : string | undefined
}

export interface NotificationState {
    list_notification : Array<Notification>
}

export function getNotificationState() : NotificationState {
    return {
        list_notification : []
    }
}
