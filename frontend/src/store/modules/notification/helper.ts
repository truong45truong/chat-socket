export interface Notification {
    id : string ,
    content : string ,
    email_user_chat : string ,
    is_chat : boolean ,
    type : string ,
    group_id : string | undefined,
    is_seem : boolean
}

export interface NotificationState {
    list_notification : Array<Notification>
    number_notification : number 
}

export function getNotificationState() : NotificationState {
    return {
        list_notification : [] ,
        number_notification : 0
    }
}
