export interface Group {
    id : string ,
    group_name : string ,
    description : string ,
    group_id : string ,
    list_message_sent: Array<any>,
    list_user_seen: Array<any>,
}

export interface GroupState {
    list_group : Array<Group>
}

export function getGroupState() : GroupState {
    return {
        list_group : []
    }
}