  function whoIam(val,email){
   opt = $(val).val();
   seller_email = 'seller_email';
   buyer_email  =  'buyer_email';
   console.log(opt)
   if(opt == 1){
    id = seller_email;
    $('#'+buyer_email).val('');
    $('#'+buyer_email).removeAttr("readonly");
   }else{
    id = buyer_email;
    $('#'+seller_email).val('');
    $('#'+seller_email).removeAttr("readonly");
   }
   $('#'+id).val(email);
   $('#'+id).attr("readonly","readonly");
  }


   $(function() {
    $('#expires').datetimepicker({
      language: 'en'
    });
    });