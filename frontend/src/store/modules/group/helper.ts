export interface Group {
    group_name : string ,
    description : string ,
    group_id : string ,
}

export interface GroupState {
    list_group : Array<Group>
}

export function getGroupState() : GroupState {
    return {
        list_group : []
    }
}