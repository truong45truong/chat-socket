import { defineStore } from 'pinia'
import { type MemberShipState , type MenberShip , getMemberShipState } from './helper'
import { store } from '@/store'


export const useMemberShipStore = defineStore('membership-store', {
  state: (): MemberShipState => getMemberShipState(),

  getters: {
    getListMemberShip(state): Array<MenberShip> {
      return state.list_membership
    },
  },

  actions: {
    uploadData(list_membership : Array<MenberShip> ) {
      let arrayList: any = []
      for(let user of list_membership){
        arrayList = [...arrayList, { 'email' : user.email , 'is_online' : false }]
      }
      this.list_membership = arrayList
    },
    checkMemberShip(user_to : MenberShip) : boolean{
        for( let item of this.list_membership){
            if(item.email == user_to) return true
        }
        return false
    },
    addFriend(friend : string ){
        
        this.list_membership = [...this.list_membership,{ email : friend} ]
    },
    removeFriend(friend : string) {
        this.list_membership = this.list_membership.filter( (item : any) => {
           if (item.email != friend) {
            return item
           }
        } )


    },
    uploadOnline(list_status : Array<any>){
      function checkOnline(email : string,list_status : Array<any>) : boolean{
        for (let user of list_status){
          if(email == user.email) { return true }
        }
        return false
      }
      let arrayList: any = []
      for (let user of this.list_membership){
          if( checkOnline(user.email , list_status) == true ){
            arrayList = [...arrayList, { 'email' : user.email , 'is_online' : true }]
          }else {
            arrayList = [...arrayList, { 'email' : user.email , 'is_online' : false }]
          }
      }
      this.list_membership = arrayList
    },
    uploadUserOnline(email : string) {
      this.list_membership = this.list_membership.filter(
        (user : any) => {
          if( user.email == email ) user.is_online = true
          return user
        }
      )
    }

  },
})

