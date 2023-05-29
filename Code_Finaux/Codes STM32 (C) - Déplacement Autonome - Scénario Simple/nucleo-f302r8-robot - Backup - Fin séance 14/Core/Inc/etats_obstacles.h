/*
 * etats_obstacles.h
 *
 *  Created on: Apr 25, 2023
 *      Author: siben
 */

#ifndef INC_ETATS_OBSTACLES_H_
#define INC_ETATS_OBSTACLES_H_

void control_etat(int *p_etat);
void etat_initial(int *p_etat);
void etat_detection_lidar(int *p_etat);
void etat_detecte_rien(int *p_etat);
void etat_destination_atteinte(int *p_etat);
void etat_QR_detecte(int *p_etat);
void etat_QR_atteint(int *p_etat);


void str_insert(char dest, char src, char *insertStr, uint16_t insertPos);


#endif /* INC_ETATS_OBSTACLES_H_ */
