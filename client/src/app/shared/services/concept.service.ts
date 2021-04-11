import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {Concept} from "../model/concept.class";

@Injectable({
  providedIn: 'root'
})
export class ConceptService {
  baseUrl: string = '/api/concept'

  constructor(private http: HttpClient) { }

  listConcept(): Observable<Concept[]> {
    return this.http.get<Concept[]>(this.baseUrl, {headers: new HttpHeaders({
        Authorization: 'Bearer ' + (localStorage.getItem('access_token') || '')
      })})
  }
}
