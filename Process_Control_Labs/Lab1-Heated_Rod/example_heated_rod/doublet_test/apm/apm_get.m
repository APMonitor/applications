% APM Retrieve File From Server
function [] = apm_get(server,app,filename)
   % get ip address for web-address lookup
   ip = deblank(urlread([deblank(server) '/ip.php']));    
   url = [deblank(server) '/online/' ip '_' app '/' filename];
   response = urlread(url);
   % write file
   fid = fopen(filename,'w');
   fwrite(fid,response);
   fclose(fid);
