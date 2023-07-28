export interface MenberShip {
    email : string
}
export interface MemberShipState {
    list_membership : Array<MenberShip>
}

export function getMemberShipState() : MemberShipState{
    return {
        list_membership : []
    }
}