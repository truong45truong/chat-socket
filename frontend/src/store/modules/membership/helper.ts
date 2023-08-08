export interface MenberShip {
    email : string
    is_online : boolean | undefined
}
export interface MemberShipState {
    list_membership : Array<MenberShip>
}

export function getMemberShipState() : MemberShipState{
    return {
        list_membership : []
    }
}