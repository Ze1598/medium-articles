import { TestBed } from '@angular/core/testing';

import { MockServ1Service } from './mock-serv-1.service';

describe('MockServ1Service', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MockServ1Service = TestBed.get(MockServ1Service);
    expect(service).toBeTruthy();
  });
});
