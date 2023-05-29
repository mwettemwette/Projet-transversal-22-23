<!DOCTYPE HTML>
    <html>
        <head>
            <title> AranaCorp </title>
            <meta http-equiv='content-type' content='text/html; charset=UTF-8'>
            <meta name='apple-mobile-web-app-capable' content='yes' />
            <meta name='apple-mobile-web-app-status-bar-style' content='black-translucent' />
            <meta http-equiv='refresh' content='10'>
            <link rel="stylesheet" href='rpi_style.css'/>
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        </head>
        
        <body bgcolor = '#70706F'> 
           <?php

           function write_command($cmd)
           {
              $file ="/var/www/html/Commandes.txt";
              $fileopen=(fopen($file,'w') or die("didn't opened the file") );
              fwrite($fileopen,$cmd);
              fclose($fileopen);

           }
              if( isset($_POST['up']) )
              {
               
                write_command("up");
              }

              if( isset($_POST['down']) )
              {
               
                write_command("down");
              }

              if( isset($_POST['right']) )
              {
               
                write_command("right");
              }
              if( isset($_POST['left']) )
              {
                write_command("left");
              }

              if( isset($_POST['stop']) )
              {
                write_command("s");
              }

              if ( isset($_POST['led_1_on']))
              {
                write_command("OPEN_CELL:1");
              }
              if ( isset($_POST['led_1_off']))
              {
                write_command("CLOSE_CELL:1");
              }

              if ( isset($_POST['led_2_on']))
              {
                write_command("OPEN_CELL:2");
              }
              if ( isset($_POST['led_2_off']))
              {
                write_command("CLOSE_CELL:2");
              }

              if ( isset($_POST['led_3_on']))
              {
                write_command("OPEN_CELL:3");
              }
              if ( isset($_POST['led_3_off']))
              {
                write_command("CLOSE_CELL:3");
              }
              
             ?>

            <hr/><hr>
            <h1 style='color : #3AAA35;'><center> Telecommande </center></h1>
            <hr/><hr>
            <br><br>
            <h2><center><p>Equipe D 3</p></center></h2>
            <br><br><h2> Commandes </h2>
            <div id='btnContainer'>
              <form method="post">
                  <center>
                  <input type="submit" name='up' value="up">
                  </center>
                  <center>
                    <input type="submit" name='down' value="down">
                  </center>
                  <center>
                    <input type="submit" name='left' value="left">
                  </center>
                  <center>
                    <input type="submit" name='right' value="right"> 
                   </center>
                   <center>
                    <input type="submit" name='stop' value="stop"> 
                   </center>
                   <p> Spots livraison</p>
                   <center>
                    <input type="submit" name='led_1_on' value="led_1_on"> 
                   </center>
                   <center>
                    <input type="submit" name='led_1_off' value="led_1_off"> 
                   </center>

                   <center>
                    <input type="submit" name='led_2_on' value="led_2_on"> 
                   </center>
                   <center>
                    <input type="submit" name='led_2_off' value="led_2_off"> 
                   </center>

                   <center>
                    <input type="submit" name='led_3_on' value="led_3_on"> 
                   </center>
                   <center>
                    <input type="submit" name='led_3_off' value="led_3_off"> 
                   </center>
                   

            </center>
              </form>
             </div>
            
    </body>
