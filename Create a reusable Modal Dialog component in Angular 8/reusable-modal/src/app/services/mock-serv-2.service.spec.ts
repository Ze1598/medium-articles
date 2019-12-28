import { TestBed } from '@angular/core/testing';

import { MockServ2Service } from './mock-serv-2.service';

describe('MockServ2Service', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MockServ2Service = TestBed.get(MockServ2Service);
    expect(service).toBeTruthy();
  });
});
