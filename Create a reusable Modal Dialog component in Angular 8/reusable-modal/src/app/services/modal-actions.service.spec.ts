import { TestBed } from '@angular/core/testing';

import { ModalActionsService } from './modal-actions.service';

describe('ModalActionsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ModalActionsService = TestBed.get(ModalActionsService);
    expect(service).toBeTruthy();
  });
});
